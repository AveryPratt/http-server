if __name__ == '__main__':
    from gevent.server import StreamServer
    from gevent.monkey import patch_all
    import server
    patch_all()
    server = StreamServer(('127.0.0.1', 10000), server.server)
    print('Starting teddy bear server on port 10000')
    server.serve_forever()
