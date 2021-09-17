from setuptools import setup

package_name = 'phidgets_python_api'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    author='Peter Polidoro',
    author_email='peter@polidoro.io',
    maintainer='Peter Polidoro',
    maintainer_email='peter@polidoro.io',
    keywords=['Phidgets','API'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Phidgets Python API',
    license='BSD',
    tests_require=['pytest'],
)
