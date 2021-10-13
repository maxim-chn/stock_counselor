import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

import { ApplicativeUser } from './user';
import { ApplicativeUserState } from './user-state';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  public user: ApplicativeUser;
  public state: Observable<ApplicativeUserState>;
  
  private _stateSource: BehaviorSubject<ApplicativeUserState>;

  constructor() {
    this.user = this.getAnonymousUser();
    this._stateSource = new BehaviorSubject<ApplicativeUserState>(ApplicativeUserState.ANONYMOUS);
    this.state = this._stateSource.asObservable();
  }

  public clearUser(): void {
    this.user = this.getAnonymousUser();
    this._stateSource.next(ApplicativeUserState.LOGGED_OUT);
  }

  public getUser(firstName: string, lastName: string, email: string): Observable<ApplicativeUser> {
    let result = new Observable<ApplicativeUser>(subscriber => {
      let user = new ApplicativeUser();
      /**
       * @TODO Http call to the applicative users service.
       */
      this.user = user;
      this._stateSource.next(ApplicativeUserState.LOGGED_IN);
      subscriber.next(user);
    });
    return result;
  }

  public isUserLoggedIn(): boolean {
    if (this.user) {
      return this.user.avatar.altText == "Anonymous user avatar";
    }
    return false;
  }

  private getAnonymousUser(): ApplicativeUser {
    /**
     * @TODO set img src of default icon.
     */
    let result = ApplicativeUser.withAllAttributes(
      0,
      "Anonymous user avatar",
      "Anonymous user img src",
      "Joe?",
      "Is that you?"
    );
    return result;
  } 
}
