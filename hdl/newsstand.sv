// Desgin the news paper vending machine
module newstand (
    input [2:0]  coin,
    input        clock,
    input        reset,
    output logic newspaper,
    output logic change
    );
    
    enum bit [2:0] {ST0, ST5, ST10, ST15, ST20} State, Next;
    enum bit [1:0] {nocoin, nickel, dime} coin_e;
    
    always_ff @(posedge clock, posedge reset)
    if (reset) State <= ST0;
    else       State <= Next;
    
    always_comb begin: set_next_state
        Next = State;
        unique case (State)
            ST0: begin
                case (coin)
                    nocoin: Next = ST0;
                    nickel: Next = ST5;
                    dime  : Next = ST10;
                    default: Next = ST0;
                endcase
            end
            ST5: begin
                case (coin)
                    nocoin: Next = ST5;
                    nickel: Next = ST10;
                    dime  : Next = ST15;
                    default: Next = ST0;
                endcase
            end
            ST10: begin
                case (coin)
                    nocoin: Next = ST10;
                    nickel: Next = ST15;
                    dime  : Next = ST20;
                    default: Next = ST0;
                endcase
            end
            ST15: begin
                Next = ST0;
            end
            ST20: begin
                Next = ST0;
            end
        endcase
    end: set_next_state
    
    always_comb begin: set_outputs
        {newspaper,change}=2'b00;
        unique case (State)
            ST0, 
            ST5, 
            ST10: {newspaper,change}=2'b00;
            ST15: {newspaper,change}=2'b10;
            ST20: {newspaper,change}=2'b11;
        endcase
    end: set_outputs
    
endmodule


