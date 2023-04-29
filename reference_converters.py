"""
reference_converters.py
=======================
Module for converting electrochemical potentials to different reference electrode scales.
"""
import pandas as pd
import numpy as np

# reference electrode potentials from Bard and Faulkner Electrochemical Methods Fundamentals and Applications 2nd Ed.
aqueous_references = {'SCE': 0.0,
                      'NHE': 0.242,
                      'SHE': 0.242,
                      'Ag|AgCl': 0.045
                    }
# reference electrode potentials from Bard and Faulkner Electrochemical Methods Fundamentals and Applications 2nd Ed.
nonaq_references = {'Fc/Fc+': 0.0,
                    'SCE': -0.31, # Bard & Faulkner
                    'NHE': -0.31 + 0.242, # Bard & Faulkner Fc vs. SCE + NHE corr
                    'SHE': -0.31 + 0.242, # Bard & Faulkner Fc vs. SCE + SHE corr
                   }

lithium_nonaq_references = {'MeCN': -3.3,
                            'acetonitrile': -3.3,
                            'carbonate (using PC)': -3.4,
                           } # values extracted from Journal of The Electrochemical Society, 164 (12) A2295-A2297 (2017)

def aqueous_potentials_to_SCE(row):
    """Takes in pd.DataFrame row or Series and converts redox_potential_V to new value vs SCE.
    This is only for aqueous media.
    
    Parameters
    ----------
    row: pd.Series
        Entry for a redox potential measured in aqueous media. Essential fields: 
        redox_potential_V (float, measured potential to convert), 
        reference_electrode (str, abbreviation describing reference electrode potential reported against).
        
    Returns
    -------
    pd.Series
        Entry for a redox potential measured in aqueous media, same format as input. 
        redox_potential converted to SCE potential scale, 
        reference_electrode updated to 'SCE'. 
        If the potential cannot be corrected, original entry returned unaltered.
    """
    ref = row.at['reference_electrode']
    if ref in aqueous_references.keys():
        correction_V = aqueous_references[ref]
        row.at['reference_electrode'] = 'SCE'
        row.at['redox_potential_V'] = row.at['redox_potential_V'] + correction_V 
        return row
    else:
        return row
    
def nonaqueous_potentials_to_Fc(row):
    """Takes in pd.DataFrame row or Series and converts redox_potential_V to new value vs. Fc/Fc+.
    This is only for non-aqueous media.
    
    Parameters
    ----------
    row: pd.Series
        Entry for a redox potential measured in aqueous media. Essential fields: 
        redox_potential_V (float, measured potential to convert), 
        reference_electrode (str, abbreviation describing reference electrode potential reported against), 
        solvent(str, name of solvent used for measurement)
        
    Returns
    -------
    pd.Series
        Entry for a redox potential measured in aqueous media, same format as input. 
        redox_potential converted to Fc/Fc+ potential scale, 
        reference_electrode updated to 'Fc/Fc+'.
        If the potential cannot be corrected, original entry returned unaltered.
    """
    ref = row.at['reference_electrode']
    if ref == 'Li|Li+':
        if row.at['solvent'] in lithium_nonaq_references.keys():
            correction_V = lithium_nonaq_references[ref]

        else:
            correction_V = lithium_nonaq_references['carbonate (using PC)']
        row.at['reference_electrode'] = 'Fc/Fc+'
        row.at['redox_potential_V'] = row.at['redox_potential_V'] + correction_V
    elif ref in nonaq_references.keys():
        correction_V = nonaq_references[ref]
        row.at['reference_electrode'] = 'Fc/Fc+'
        row.at['redox_potential_V'] = row.at['redox_potential_V'] + correction_V
    return row