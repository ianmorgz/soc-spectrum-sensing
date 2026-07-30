# define the state machine for the algorithm
class Transition:
    def __init__(self, from_state, to_state, condition, additional_actions=None):
        self.from_state = from_state
        self.to_state = to_state
        self.condition = condition
        self.additional_actions = additional_actions

class FSSStateMachine:
    # define the states of the state machine
    SEARCH = 0
    FILL_BUCKET_1 = 1
    FILL_BUCKET_2 = 2

    def __init__(self):
        self.states = ["SEARCH", "FILL BUCKET 1", "FILL BUCKET 2"]
        self.current_state = 0

        # algorithm parameters (these are used and changed by the state machine)
        self.packet_count = 0
        self.b1_start = 0
        self.b1_size = 0
        self.b2_start = 0
        self.b2_size = 0
        self.threshold = 0 # dB threshold for the FSS detection algorithm. Make sure to update this with the proper threshold

        self.state_transitions = [[
            # ========== SEARCH STATE TRANSITION ==========
            Transition(
                0, 
                0, 
                (lambda x: x > self.threshold), 
                (self.s_to_s)
            ), 
            Transition(
                0, 
                1, 
                (lambda x: x <= self.threshold and self.b1_size <= self.b2_size), 
                (self.s_to_fb1)
            ),
            Transition(
                0, 
                2, 
                (lambda x: x <= self.threshold and self.b1_size > self.b2_size), 
                (self.s_to_fb2)
            )
        ], [
            # ========== FILL BUCKET 1 STATE TRANSITION ==========
            Transition(
                1, 
                1, 
                (lambda x: x <= self.threshold), 
                (self.fb1_to_fb1)
            ),
            Transition(
                1, 
                0, 
                (lambda x: x > self.threshold), 
                (self.fb1_to_s)
            )
        ], [
            # ========== FILL BUCKET 2 STATE TRANSITION ==========
            Transition(
                2, 
                2, 
                (lambda x: x <= self.threshold), 
                (self.fb2_to_fb2)
            ),
            Transition(
                2, 
                0, 
                (lambda x: x > self.threshold), 
                (self.fb2_to_s)
            )
        ]]

    # ========== SEARCH STATE TRANSITION ACTIONS ==========

    def s_to_s(self):
        self.packet_count += 1

    def s_to_fb1(self):
        self.b1_start = self.packet_count
        self.b1_size = 1
        self.packet_count += 1

    def s_to_fb2(self):
        self.b2_start = self.packet_count
        self.b2_size = 1
        self.packet_count += 1

    # ========== FILL BUCKET 1 STATE TRANSITION ACTIONS ==========

    def fb1_to_fb1(self):
        self.b1_size += 1
        self.packet_count += 1

    def fb1_to_s(self):
        self.packet_count += 1

    # ========== FILL BUCKET 2 STATE TRANSITION ACTIONS ==========
    def fb2_to_fb2(self):
        self.b2_size += 1
        self.packet_count += 1

    def fb2_to_s(self):
        self.packet_count += 1    

    # ========== STATE MACHINE METHODS ==========
    def cycle(self, input):
        current_state_transitions = self.state_transitions[self.current_state]

        for transition in current_state_transitions:

            if(transition.from_state != self.current_state):
                raise ValueError(f"Transition from state {transition.from_state} does not match current state {self.current_state}")

            if transition.condition(input):
                self.current_state = transition.to_state
                if transition.additional_actions:
                    transition.additional_actions()

                return

        raise ValueError(f"No valid transition found for input {input} in state {self.current_state}")

    # used in place of a reset flag
    def RESET(self):
        if self.b1_size >= self.b2_size:
            temp = (self.b1_start, self.b1_size)
        else:
            temp = (self.b2_start, self.b2_size)
        
        self.current_state = 0
        self.packet_count = 0
        self.b1_start = 0
        self.b1_size = 0
        self.b2_start = 0
        self.b2_size = 0

        return temp