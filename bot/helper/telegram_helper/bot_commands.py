from bot.get_config import getConfig

class _BotCommands:
    def __init__(self):
        self.StatsCommand = getConfig(
            "COMMANDI_STATS",
            "stats"
        )
        self.StartCommand = getConfig(
            "COMMANDI_START",
            "start"
        )
        self.RestartCommand = getConfig(
            "COMMANDI_RESTART",
            "restart"
        )
        self.PingCommand = getConfig(
            "COMMANDI_PING",
            "ping"
        )
        self.LogCommand = getConfig(
            "COMMANDI_LOG",
            "log"
        )
        self.HelpCommand = getConfig(
            "COMMANDI_HELP",
            "help"
        )
        self.MirrorCommand = getConfig(
            "COMMANDI_MIRROR",
            "mirror"
        )
        self.TarMirrorCommand = getConfig(
            "COMMANDI_TARMIRROR",
            "tarmirror"
        )
        self.WatchCommand = getConfig(
            "COMMANDI_WATCH",
            "watch"
        )
        self.TarWatchCommand = getConfig(
            "COMMANDI_TARWATCH",
            "tarwatch"
        )
        self.CloneCommand = getConfig(
            "COMMANDI_CLONE",
            "clone"
        )
        self.UnzipMirrorCommand = getConfig(
            "COMMANDI_UNZIPMIRROR",
            "unzipmirror"
        )
        self.CancelMirror = getConfig(
            "COMMANDI_CANCEL",
            "cancel"
        )
        self.CancelAllCommand = getConfig(
            "COMMANDI_CANCELALL",
            "cancelall"
        )
        self.ListCommand = getConfig(
            "COMMANDI_LIST",
            "list"
        )
        self.StatusCommand = getConfig(
            "COMMANDI_STATUS",
            "status"
        )
        self.EvalCommand = getConfig(
            "COMMANDI_EVAL",
            "eval"
        )
        self.ExecCommand = getConfig(
            "COMMANDI_EXEC",
            "exec"
        )


BotCommands = _BotCommands()
