pragma solidity >=0.4.0 <0.7.6;

contract Model {

    enum states {training, aggregation, finished}
    states public state;

    string public configurationAddress;
    string public weightsAddress;
    string public scriptsAddress;

    uint public current_epoch;
    uint public target_epoch;

    uint private updatesTillAggregation;
    uint private consensusThreshold;
    mapping(string => uint) private aggregationVotes;
    string private currentCandidate;
    uint private submittedVotes;
    string[] private votedAddresses;

    struct Submission {
        address trainer;
        string storageAddress;
    }

    Submission[] public localUpdates;
    mapping(address => bool) private trainers;
    address[] private trainerArray;                     //Array for looping the rightToVote mapping
    mapping(address => bool) private rightToVote;      //Should be true for trainers that have the right to vote (has not voted yet)

    modifier isTrainer()
    {
        require(trainers[msg.sender], "Not an authorized trainer");
        _;
    }

    modifier atState(states _state)
    {
        require(_state == state, "Not valid at this state");
        _;
    }

    modifier hasNotVoted()
    {
        require(rightToVote[msg.sender], "Already submitted/voted this epoch");
        _;
    }

    constructor(
        string memory _configurationAddress,
        string memory _weightsAddress,
        string memory _scriptsAddress,
        uint _updatesTillAggregation,
        uint _consensusThreshold,
        uint _target_epoch) public
    {
        configurationAddress = _configurationAddress;
        weightsAddress = _weightsAddress;
        scriptsAddress = _scriptsAddress;
        updatesTillAggregation = _updatesTillAggregation;
        consensusThreshold = _consensusThreshold;
        current_epoch = 0;
        target_epoch = _target_epoch;
        state = states.training;
        trainers[msg.sender] = true;
        trainerArray.push(msg.sender);
        rightToVote[msg.sender] = true;
    }

    function addTrainer(address trainer)
    public
    isTrainer()
    {
        trainers[trainer] = true;
        trainerArray.push(trainer);
        rightToVote[trainer] =true;
    }

    function submitLocalUpdate(string memory updateAddress)
    public
    isTrainer()
    hasNotVoted()
    atState(states.training)
    {
        localUpdates.push(Submission(msg.sender, updateAddress));
        rightToVote[msg.sender] = false;
        if (localUpdates.length >= updatesTillAggregation) {
            state = states.aggregation;
            //Reset rightToVote before aggregation
            for(uint i=0; i<trainerArray.length; i++){
                rightToVote[trainerArray[i]] = true;
            }
        }
    }

    // Needed to retrieve all local updates programmatically
    function LocalUpdatesCount()
    public
    view
    returns (uint) {
        return localUpdates.length;
    }

    function submitLocalAggregation(string memory updateAddress)
    public
    isTrainer()
    hasNotVoted()
    atState(states.aggregation)
    {
        aggregationVotes[updateAddress] = aggregationVotes[updateAddress] + 1;
        submittedVotes = submittedVotes + 1;
        votedAddresses.push(updateAddress);
        rightToVote[msg.sender] = false;

        // Update best candidate if needed
        if (aggregationVotes[updateAddress] > aggregationVotes[currentCandidate]) {
            currentCandidate = updateAddress;
        }

        // Find consensus if enough votes came in
        if (aggregationVotes[currentCandidate] >= consensusThreshold || submittedVotes >= updatesTillAggregation) {

            weightsAddress = currentCandidate;
            current_epoch = current_epoch + 1;

            // Reset submissions (aggregation & training)
            submittedVotes = 0;
            while(votedAddresses.length > 0) {
                aggregationVotes[votedAddresses[votedAddresses.length-1]] = 0;
                votedAddresses.pop();
            }
            while(localUpdates.length > 0){
                localUpdates.pop();
            }
            // Reset voting rights
            for(uint i=0; i<trainerArray.length; i++){
                rightToVote[trainerArray[i]] = true;
            }

            if(current_epoch < target_epoch){
                state = states.training;
            } else {
                state = states.finished;
            }
        }
    }
}