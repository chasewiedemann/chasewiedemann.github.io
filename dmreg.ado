capture program drop dmreg
discard
program define dmreg, rclass
    version 16.0
    // Syntax for the program
   syntax,  d(varlist) x(varlist) z(varlist) fe(varlist) /// 
		[useCartesian(numlist integer max = 1) ///
		useFEInteractions(numlist integer max = 1) ///
		numChunks(numlist integer max = 1) ///
		useInteractedZ(numlist integer max = 1) ///
		useCUE(numlist integer max = 1) ///
		useNormalDist(numlist integer max = 1) ///
		useDiagonalSigma(numlist integer max = 1) ///
		numInferenceDraws(numlist integer max = 1) ///
		usePsi1(numlist integer max = 1) ///
		estimateUncmin(numlist integer max = 1) ///
		testType(string) ///
		sFunction(string) ///
		] ///
		 			     

   javacall dm.StataLink reg, jar(Distribution.jar)
   discard

end program
