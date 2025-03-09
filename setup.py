from setuptools import setup, find_packages

setup(
    name="newsletter",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn",
        "openai",
        "python-dotenv",
        "pydantic",
        "rich",
    ],
    python_requires=">=3.10",
    author="Your Name",
    author_email="your.email@example.com",
    description="An AI-powered newsletter generation system",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bybysker/newsletter-generator",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
) 