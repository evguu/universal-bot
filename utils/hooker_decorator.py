from utils.hookers import Hooker


def multipart_input(req, args, *hooker_args):
    def wrapper(func):
        hooker = Hooker(req.user, func, *hooker_args)
        if len(args):
            for i, arg in enumerate(args):
                greed_flag = False
                if hooker.func_args[0].greedy:
                    arg = " ".join(args[i:])
                    greed_flag = True
                try:
                    hooker_response = hooker.arg_read(arg, message_id=req.message_id, presend=True)
                except AttributeError:
                    hooker_response = hooker.arg_read(arg, presend=True)
                if not hooker_response:
                    return
        hooker.init(getattr(req, "message_id", None))
        return func

    return wrapper
