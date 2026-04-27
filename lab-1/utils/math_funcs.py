class MathFunctions:

    @staticmethod
    def clip_left(x: float, x_clip: float) -> float:
        """"""
        return x_clip if x < x_clip else x

    @staticmethod
    def clip_right(x: float, x_clip: float) -> float:
        """"""
        return x_clip if x > x_clip else x

    @staticmethod
    def clip(x: float, x_left: float, x_right: float) -> float:
        """"""
        return MathFunctions.clip_right(MathFunctions.clip_left(x, x_left), x_right)
