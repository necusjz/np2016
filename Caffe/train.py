import caffe

caffe.set_mode_cpu()
solver = caffe.get_solver('lenet_solver.prototxt')
#solver.snapshot('lenet_iter_10000.caffemodel')
solver.solve()
