o = {
    "a": 97,
    "b": 98,
    "c": 99,
    "d": 100,
    "我": "我不会再回头"
}

if __name__ == '__main__':
    import timeit

    print(timeit.timeit("pickle.dumps(o)", globals=globals(), number=10000))

    print(timeit.timeit("json.dumps(o)", globals=globals(), number=10000))

    print(timeit.timeit("gzip.compress(json.dumps(o))", globals=globals(), number=10000))

    # 结论，pickle比json快
