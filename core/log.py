# log.py — 日志与调试模块
"""统一的日志记录，支持文件输出和终端输出。"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional

# 日志文件路径（程序根目录）
_log_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_log_file = os.path.join(_log_dir, "ustPlayer.log")

# 全局 logger
_logger: Optional[logging.Logger] = None


def _build_logger() -> logging.Logger:
    """构建并配置 logger。"""
    logger = logging.getLogger("ustPlayer")
    logger.setLevel(logging.DEBUG)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 文件 handler — 详细日志
    fh = logging.FileHandler(_log_file, encoding="utf-8", mode="a")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s:%(lineno)d — %(message)s",
        datefmt="%H:%M:%S",
    ))
    logger.addHandler(fh)

    # 控制台 handler — INFO 及以上
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    ))
    logger.addHandler(ch)

    return logger


def get_logger() -> logging.Logger:
    """获取全局 logger 实例。"""
    global _logger
    if _logger is None:
        _logger = _build_logger()
    return _logger


def log_startup():
    """记录程序启动信息。"""
    logger = get_logger()
    logger.info("=" * 50)
    logger.info(f"ustPlayer 启动 — {datetime.now().isoformat()}")
    logger.info(f"Python: {sys.version}")
    logger.info(f"工作目录: {os.getcwd()}")
    logger.info(f"日志文件: {_log_file}")
    try:
        from PySide6.QtCore import QLibraryInfo, qVersion
        logger.info(f"Qt 版本: {qVersion()}")
    except Exception:
        pass


def log_exception(msg: str = ""):
    """便捷方法：记录异常堆栈。"""
    get_logger().exception(msg)
