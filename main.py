import graf_gen as gr
import ant_alg as ant

n = 10  # количество точек
alpha = 1  # значимость феромонов (в какую степень возводим)
beta = 1  # значимость расстояния (в какую степень возводим)
Q = 2  # количесиво фермонона на путь
p = 0.4  # испаряемость феромона
t0 = 0.2  # изначательное количество феромона
It = 7000  # количество итераций

feromon_matrix = ant.create_feromon_matrix(n, t0)
distance_matrix = ant.create_distance_matrix(n)


if __name__ == '__main__':
    for i in range(It):
        feromon_matrix = ant.do_all_ants_circle(feromon_matrix, distance_matrix, Q, p, alpha, beta, n)
    gr.show_graph(gr.generate_graf(n), gr.generate_graf_width(feromon_matrix, n), None)