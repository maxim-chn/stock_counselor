import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';
import { InvestmentFunctionalitiesMenuState } from './state';

@Injectable({
  providedIn: 'root'
})
export class InvestmentFunctionalitiesMenuStateService {

  public state: Observable<InvestmentFunctionalitiesMenuState>;

  private _stateSource: BehaviorSubject<InvestmentFunctionalitiesMenuState>;

  constructor() {
    this._stateSource = new BehaviorSubject<InvestmentFunctionalitiesMenuState>(
      InvestmentFunctionalitiesMenuState.INITIAL
    );
    this.state = this._stateSource.asObservable();
  }

  public calculateInvestmentRecommendation(): void {
    this._stateSource.next(InvestmentFunctionalitiesMenuState.COLLECT_STOCK_DATA);
  }

  public collectStockData(): void {
    this._stateSource.next(InvestmentFunctionalitiesMenuState.COLLECT_STOCK_DATA);
  }
}
