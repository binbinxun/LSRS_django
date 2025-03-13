class myValueError(ValueError):
    def __init__(self, *args, **kwargs):
        self.info = kwargs.pop('info', None)  # 从 kwargs 提取 info 后删除
        super().__init__(*args, **kwargs)

