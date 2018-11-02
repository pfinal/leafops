def to_dict(model, columns=None, append_columns=None):
    '''model to dict'''
    from sqlalchemy.orm import class_mapper
    def to_str(o):
        # 对应 json 的 int float null
        if (isinstance(o, int) or isinstance(o, float) or o == None):
            return o

        # 如果不转为字符串，datetime类型无法直接序列化为json
        return str(o)

    if columns == None:
        columns = [c.key for c in class_mapper(model.__class__).columns]

    if append_columns is not None:
        columns += append_columns

    return dict((c, to_str(getattr(model, c))) for c in columns)
