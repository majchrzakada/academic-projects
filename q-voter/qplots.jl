using Plots
using DelimitedFiles

voter1 = readdlm("N100dx002L1000.txt")
xs = voter1[1:51]
p1 = voter1[52:102]
t1 = voter1[103:153]

voter2 = readdlm("N200dx002L1000.txt")
p2 = voter2[52:102]
t2 = voter2[103:153]

voter3 = readdlm("N300dx002L1000.txt")
p3 = voter3[52:102]
t3 = voter3[103:153]

probs = plot(p1, xticks = ([1, 8, 15, 22, 29, 36, 43, 51], [xs[1], xs[8], xs[15], xs[22], xs[29], xs[36], xs[43], xs[51]]), 
title="Positive consensus probability for L=1000", titlefont=font(10), legend=:bottomright,
linecolor=:lightsalmon, marker=(:diamond, :lightsalmon), markerstrokecolor=:lightsalmon, xlabel="x", ylabel="P", label="N=100")
plot!(p2, label="N=200", marker=(:star7, :tomato), markerstrokecolor=:tomato, linecolor=:tomato)
plot!(p3, label="N=300", marker=(:star5, :red4), markerstrokecolor=:red4, linecolor=:red4)
savefig(probs, "probs.png")

times = plot(t1, xticks = ([1, 8, 15, 22, 29, 36, 43, 51], [xs[1], xs[8], xs[15], xs[22], xs[29], xs[36], xs[43], xs[51]]), 
title="Average time needed to reach consensus for L=1000", titlefont=font(10), linecolor=:lightsalmon,
marker=(:diamond, :lightsalmon), markerstrokecolor=:lightsalmon, xlabel="x", ylabel="t", label="N=100")
plot!(t2, label="N=200", marker=(:star7, :tomato), markerstrokecolor=:tomato, linecolor=:tomato)
plot!(t3, label="N=300", marker=(:star5, :red4), markerstrokecolor=:red4, linecolor=:red4)
savefig(times, "times.png")