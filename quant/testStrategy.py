import quantPy as qp
import ysq
import wIndicators as wI
import argparse

def runStrategy(strategy):
<<<<<<< HEAD
<<<<<<< HEAD
	if strategy == 'meanReversion':
=======
  if strategy == 'meanReversion':
>>>>>>> 732e452f960bbb11686e96834d43562b6e8b44c9
=======
  if strategy == 'meanReversion':
>>>>>>> 732e452f960bbb11686e96834d43562b6e8b44c9
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
<<<<<<< HEAD
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> 732e452f960bbb11686e96834d43562b6e8b44c9
=======
    main()
>>>>>>> 732e452f960bbb11686e96834d43562b6e8b44c9
