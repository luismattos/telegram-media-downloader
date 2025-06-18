"""
Setup script for Telegram Media Downloader package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="telegram-media-downloader",
    version="2.0.0",
    author="Luis Mattos",
    author_email="luis@example.com",
    description="Um downloader de mídia e mensagens para Telegram com suporte a downloads incrementais",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/luismattos/telegram-media-downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Communications :: Chat",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "telegram-downloader=telegram_media_downloader.core.downloader:run_downloader",
            "telegram-list-chats=telegram_media_downloader.core.chat_lister:run_chat_lister",
            "telegram-interactive=telegram_media_downloader.core.interactive:main_interactive",
        ],
    },
    include_package_data=True,
    package_data={
        "telegram_media_downloader": ["*.md", "*.txt"],
    },
    keywords="telegram, downloader, media, messages, chat, channel, group",
    project_urls={
        "Bug Reports": "https://github.com/luismattos/telegram-media-downloader/issues",
        "Source": "https://github.com/luismattos/telegram-media-downloader",
        "Documentation": "https://github.com/luismattos/telegram-media-downloader#readme",
    },
) 