# setup.py

from setuptools import setup, find_packages

setup(
    name='telegram_notifier',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    data_files=[
        ('telegram_notifier', ['telegram_notifier/.env']),
    ],
    author='Matteo Vilucchio',
    author_email='your.email@example.com',
    description='A package to notify via Telegram when a simulation starts and finishes.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mvilucchio/TelegramNotifier',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
