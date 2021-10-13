import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

import { WebsiteMenuState } from './state';

@Injectable({
  providedIn: 'root'
})
export class WebsiteMenuStateService {

  public state: Observable<WebsiteMenuState>;

  private _stateSource: BehaviorSubject<WebsiteMenuState>;

  constructor() {
    this._stateSource = new BehaviorSubject<WebsiteMenuState>(WebsiteMenuState.INITIAL);
    this.state = this._stateSource.asObservable();
  }

  public loginState(): void {
    this._stateSource.next(WebsiteMenuState.LOGIN);
  }

  public initialState(): void {
    this._stateSource.next(WebsiteMenuState.INITIAL);
  }

  public signupState(): void {
    this._stateSource.next(WebsiteMenuState.SIGNUP);
  }
}
