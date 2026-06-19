# log.py — 日志模块（基于 loguru）
"""统一的日志记录，基于 loguru，支持文件轮转和控制台彩色输出。

用法:
    from core.log import logger, log_startup

    logger.info("正常信息")
    logger.debug("调试信息")
    logger.exception("异常信息（自动附堆栈）")
"""

import sys
import os

from loguru import logger as _logger

# 移除默认 handler
_logger.remove()

# 日志文件路径
_log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_log_file = os.path.join(_log_dir, "ustPlayer.log")

# 文件输出：DEBUG 级别，UTF-8，自动轮转
_logger.add(
    _log_file,
    level="DEBUG",
    encoding="utf-8",
    rotation="1 MB",
    retention="7 days",
    format="{time:HH:mm:ss} [{level}] {name}:{function}:{line} — {message}",
)

# 控制台输出：INFO 级别，彩色
_logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> [<level>{level}</level>] {message}",
)

# 暴露为模块级 logger，直接使用
logger = _logger


def log_startup():
    """记录程序启动信息。"""
    logger.info("=" * 50)
    logger.info("ustPlayer 启动")
    logger.info(f"Python: {sys.version}")
    logger.info(f"工作目录: {os.getcwd()}")
    logger.info(f"日志文件: {_log_file}")
    try:
        from PySide6.QtCore import qVersion
        logger.info(f"Qt 版本: {qVersion()}")
    except Exception:
        pass


def get_logger():
    """兼容旧接口，返回全局 logger 实例。"""
    return logger
