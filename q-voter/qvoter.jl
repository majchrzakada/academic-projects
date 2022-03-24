using DelimitedFiles
using LaTeXStrings
using StatsBase


"""
    Initial state of the system.
    
    Args:
        N - size
        x - initial positive opinions accumulation
"""
function initial_state(N, x)
    state = -ones(Int, (1,N))
    positive_num = Int(floor(x*N))
    positive_pos = sample(1:N, positive_num, replace=false)
    for pos in positive_pos
        state[pos] = 1
    end
    return state
end


"""
    Random choice of one of the currently considered agents.
    
    Args:
        state - current system state
        i - agent's index
"""
function choose_neighbor(state, i)
    N = size(state)[2]
    j = rand([i-1, i+1])
    if j == 0 
        neighbor = state[N]
    elseif j == N+1
        neighbor = state[1]
    else
        neighbor = state[j]
    end
    return neighbor
end


"""
    One Monte Carlo stem in q-voter model.
    
    Args:
        state - current system state
"""
function mcs(state)
    N = size(state)[2]
    for n in 1:N
        i = rand(1:N)
        neighbor = choose_neighbor(state, i)
        state[i] = neighbor
    end
    return state
end 


"""
    System evolution for given positive opinions accumulation in q-voter model.
    
    Args:
        N - size
        x - initial positive opinions accumulation
        L - number of Monte Carlo steps
"""
function q_evolve(N, x, L)
    positive = 0
    times = 0
    for l in 1:L
        state = initial_state(N, x)
        time = 0
        while (all(==(1), state) | all(==(-1), state)) == false
            evolve = mcs(state)
            state = evolve
            time += 1
        end
        times += time
        if all(==(1), state) 
            positive += 1
        end
    end
    prob = positive/L
    avg_time = times/L
    return prob, avg_time
end


"""
    Q-voter model for given vector of initial positive opinions accumulation.
    
    Args:
        N - size
        dx - positive opinions accumulation difference
        L - number of Monte Carlo steps
"""
function q_voter(N, dx, L)
    xs = 0:dx:1
    xs = [x for x in xs]
    probs = zeros(length(xs), 1)
    times = zeros(length(xs), 1)
    for i in 1:length(xs)
        prob, time = q_evolve(N, xs[i], L)
        probs[i] = prob
        times[i] = time
    end
    voter = [xs probs times]
    writedlm("N$N.dx$dx.L$L.txt", voter, " "*" ")
    return xs, probs, times
end

q_voter(100, 0.02, 1000)
q_voter(200, 0.02, 1000)
q_voter(300, 0.02, 1000)

