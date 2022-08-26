from numpy import void
from investments import investments
from installments import installments
import numpy_financial as npf

from datetime import datetime, timedelta


def order_movements(cashflows:dict, reverse_sort: bool=False) -> dict:
    """
    Normaliza a lista das datas do inicio ao final da movimentação\n
    Preenche com valor 0 todo dia sem movimentação\n
    Realiza ordenação(asc/desc) por data
    
    Parameters: reverse_sort
    
    Returns:
        dict: { '%Y-%m-%d',float }
    """
    start_date = datetime.strptime(min(cashflows, key=lambda x: datetime.strptime(x, "%Y-%m-%d")), "%Y-%m-%d")
    end_date = datetime.strptime(max(cashflows, key=lambda x: datetime.strptime(x, "%Y-%m-%d")), "%Y-%m-%d")
    intervalo=abs((end_date - start_date).days+1)
 
       
    date_list=dict(map(lambda x:((start_date + timedelta(days=x)).strftime("%Y-%m-%d"),0),range(intervalo)))
    
    if reverse_sort:
        date_list.reverse()
        
    date_list.update(cashflows)

    return date_list

def pipeline_data(cashflows:dict={}) -> list:
    """Pipeline de execução ETL like

    Returns:
        dict: _description_
    """
    #passo 1
    cashflows.update(dict(map(lambda x:  (x['created_at'], -float(x['amount'])+cashflows.get(x['created_at'],0)), investments)))

    #passo 2
    cashflows.update(dict(map(lambda x:  (x['due_date'], float(x['amount'])+cashflows.get(x['due_date'],0)), installments)))

    result=order_movements(cashflows, False) 

    return (list(map(lambda x: result[x], result)))
   
def calc_irr(data:dict) -> None:
    irr = round(npf.irr(data)*100, 2)
    print(f"TIR: {irr}%")
            
if __name__ == "__main__":
    data=pipeline_data() 
    calc_irr(data)