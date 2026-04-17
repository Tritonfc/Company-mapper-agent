from src.exa.models import PersonSearchResult
from src.workflows.models import VerificationResult
from src.workflows.models import RankedPersonResult
from src.github.signal_detector import SignalStrength

def score_person(candidate:PersonSearchResult,companies:list[VerificationResult])->RankedPersonResult:
    candidate_previous_companies =  [
           work.company.name                                                     
          for entity in candidate.entities                                      
          for work in (entity.properties.work_history or [])            
    ]
    
    matching_companies = [                                                        
      c for c in companies                                                      
      if c.company in candidate_previous_companies                              
    ] 
    
    rank_score = 0.0


    for company in matching_companies:
        if company.signal_strength == SignalStrength.STRONG:
            rank_score += 3.0
        
        elif company.signal_strength == SignalStrength.WEAK:
            rank_score +=2.0
            
        else:
            rank_score += 1.0
            
    return RankedPersonResult(
        **candidate.model_dump(), pointScore= rank_score
        
    )
    
    
    
    
    
    
    


def rank(candidates:list[RankedPersonResult])->list[RankedPersonResult]:
    sorted_list = sorted(candidates, key=lambda x: x.pointScore, reverse=True) 
    return sorted_list  
    
    
    
    
    
    