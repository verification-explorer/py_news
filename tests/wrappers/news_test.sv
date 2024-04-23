module news_test (
    input [1:0]  vif_coin,
    output logic clock,
    input        reset,
    output logic vif_newspaper,
    output logic vif_change
    );

    newstand dut (
    .coin(vif_coin),
    .clock(clock),
    .reset(reset),
    .newspaper(out_newspaper),
    .change(out_change)
    );

    initial begin
        $dumpfile("news.vcd");
        $dumpvars;
        clock=0;
        forever #5 clock=~clock;
    end
endmodule