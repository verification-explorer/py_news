module news_test (
    input [2:0]  coin,
    output logic clock,
    input        reset,
    output logic newspaper,
    output logic change
    );

    newstand dut (
    .coin(coin),
    .clock(clock),
    .reset(reset),
    .newspaper(newspaper),
    .change(change)
    );

    initial begin
        $dumpfile("news.vcd");
        $dumpvars;
        clock=0;
        forever #5 clock=~clock;
    end
endmodule