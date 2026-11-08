"""
配置管理模块
"""
import yaml
import os
from src.core.logger import logger
from src.core.exceptions import ConfigError
def get_default_config():
    default_yaml_path = "./config/default.yaml"
    if os.path.exists(default_yaml_path):
        try:
            with open(default_yaml_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except (OSError, UnicodeDecodeError, yaml.YAMLError):
            print(f"未成功加载{default_yaml_path}，使用内置配置")
            pass
    return {
        "paths": {
            "source_image": "examples/image_test.png",
            "driven_audio": "examples/audio_test.wav",
            "sadtalker_path": "../SadTalker",
            "gfpgan_model_path": "checkpoints/GFPGANv1.4.pth",
            "realesrgan_model_path": "checkpoints/RealESRGAN_x4plus.pth"
        },
        "render": {
            "preprocess": "full",
            "still": True,
            "use_enhancer": False
        },
        "enhancements": {
            "superres": False,
            "method": "fast"
        },
        "audit": {
            "lipsync_threshold": 0.6
        }
    }

class ConfigManager:
    def __init__(self, config_file=None, cli_args=None):
        self.config_file = config_file
        self.cli_args = cli_args or {}
        self._config = {}
        self.load_config()

    def load_config(self):
        self._config = get_default_config()
        logger.info("已加载默认配置")
        if self.config_file and os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    custom_config = yaml.safe_load(f) or {}
                self._config = self._merge_dict(self._config, custom_config)
                logger.info(f"自定义配置文件已加载并合并: {self.config_file}")
            except yaml.YAMLError as e:
                error_msg = f"YAML配置文件格式错误: {e}"
                logger.error(error_msg)
                raise ConfigError(error_msg) from e
            except Exception as e:
                error_msg = f"配置文件加载失败: {e}"
                logger.error(error_msg)
                raise ConfigError(error_msg) from e
        elif self.config_file:
            logger.warning(f"指定的配置文件不存在: {self.config_file}，将使用默认配置")
        if self.cli_args:
            self._apply_cli_overrides(self.cli_args)
            logger.info("已应用命令行参数覆盖")

    def _merge_dict(self, base_dict, override_dict):
        result = base_dict.copy()
        for key, value in override_dict.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_dict(result[key], value)
            else:
                result[key] = value
        return result

    def _apply_cli_overrides(self, cli_args):
        cli_config = {}
        if hasattr(cli_args, 'source_image') and cli_args.source_image:
            cli_config.setdefault('paths', {})['source_image'] = cli_args.source_image
        if hasattr(cli_args, 'driven_audio') and cli_args.driven_audio:
            cli_config.setdefault('paths', {})['driven_audio'] = cli_args.driven_audio
        if hasattr(cli_args, 'output_dir') and cli_args.output_dir:
            cli_config.setdefault('paths', {})['output_path'] = cli_args.output_dir
        if hasattr(cli_args, 'method') and cli_args.method:
            cli_config.setdefault('enhancements', {})['method'] = cli_args.method
        if hasattr(cli_args, 'upscale') and cli_args.upscale:
            cli_config.setdefault('enhancements', {})['superres'] = True
        if hasattr(cli_args, 'no_audit') and cli_args.no_audit:
            cli_config.setdefault('audit', {})['skip_audit'] = True
        self._config = self._merge_dict(self._config, cli_config)

    def get(self, key, default=None):
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key, value):
        keys = key.split('.')
        config_ref = self._config
        for k in keys[:-1]:
            if k not in config_ref or not isinstance(config_ref[k], dict):
                config_ref[k] = {}
            config_ref = config_ref[k]
        config_ref[keys[-1]] = value

    def save_config(self, filepath=None):
        filepath = filepath or self.config_file or "default.yaml"
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
            logger.info(f"配置已保存到: {filepath}")
        except Exception as e:
            logger.error(f"配置保存失败: {e}")
            raise ConfigError(f"配置保存失败: {e}") from e
