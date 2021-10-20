import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

import { ApplicativeUser } from './user';
import { ApplicativeUserState } from './user-state';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  public className: string;
  public user: ApplicativeUser;
  public state: Observable<ApplicativeUserState>;
  
  private _stateSource: BehaviorSubject<ApplicativeUserState>;

  constructor() {
    this.className = UserService.name;
    this.user = this.getAnonymousUser();
    this._stateSource = new BehaviorSubject<ApplicativeUserState>(ApplicativeUserState.ANONYMOUS);
    this.state = this._stateSource.asObservable();
  }

  public hasLoggedIn(val: ApplicativeUser): void {
    this.user = val;
    this._stateSource.next(ApplicativeUserState.LOGGED_IN);
  }
  
  public hasSignedUp(val: ApplicativeUser): void {
    this.user = val;
    this._stateSource.next(ApplicativeUserState.LOGGED_IN);
  }
  
  public logout(): void {
    this.user = this.getAnonymousUser();
    this._stateSource.next(ApplicativeUserState.LOGGED_OUT);
  }

  private getAnonymousUser(): ApplicativeUser {
    /**
     * @TODO set img src of default icon.
     */
    let result = ApplicativeUser.withAllAttributes(
      0,
      "Anonymous user avatar",
      "data:image/png;base64,BROKEN_VALUE",
      "some.user@domain.com",
      "Some",
      "User"
    );
    return result;
  } 
}
