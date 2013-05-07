import quantPy as qp
import ysq
import wIndicators as wI
import argparse

def runStrategy(strategy):
	if strategy == 'meanReversion':
		qp.spPicker(wI.meanReversion)
	elif strategy == 'roundNumbers':
		qp.spPicker(wI.roundNumbers)
	else:
		print('Invalid Strategy selected. Current valid strategies: meanReversion, roundNumbers')

def main():
	parser = argparse.ArgumentParser(description='process strategy')
	parser.add_argument('strategy', help='Strategy name you want to test', default='meanReversion', nargs='?')
	args = parser.parse_args()
	runStrategy(args.strategy)

if __name__ == "__main__":
    main()
