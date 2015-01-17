import os

def getCacheFileName():
	return 'previous-hp-info.json'

def getCacheFileForWrite():
	return open(getCacheFileName(), 'w')

def getCacheFileForRead():
	return open(getCacheFileName(), 'r')
