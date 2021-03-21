import os

if __name__ == "__main__":
    params = [('1', 'wwgamma_final_5f_NLO'),
        ('2', 'wwgamma_5f_NLO_com'),
        ('3', 'wwa_nofsr_5f_LO'),
    ]

    # loop over parameters to be restricted
    for ipar,param in enumerate(params):
        # 1D cards
        process='submit_'+ params[ipar][1]+'.jdl'
        os.system('condor_submit {0}'.format(process))
        
