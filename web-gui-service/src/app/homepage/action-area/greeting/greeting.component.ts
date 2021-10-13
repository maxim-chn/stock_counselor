import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoggerService } from 'src/app/logger.service';
import { UserService } from '../../user.service';
import { ApplicativeUserState } from '../../user-state';
import { GreetingForGuestDirective } from './greeting-for-guest.directive';
import { GreetingForUserDirective } from './greeting-for-user.directive';

@Component({
  selector: 'action-area-greeting',
  templateUrl: './greeting.component.html',
  styleUrls: ['./greeting.component.sass']
})
export class GreetingComponent implements OnInit, OnDestroy {

  public guestParagraphs: Array<string>;
  public userParagraphs: Array<string>;
  
  private userState: Subscription;

  constructor(
    private greetingForGuest: GreetingForGuestDirective,
    private greetingForUser: GreetingForUserDirective,
    private loggerService: LoggerService,
    private userService: UserService
    ) {
      this.guestParagraphs = [];
      this.userParagraphs = [];
      this.userState = new Subscription();
      this.initGuestParagraphs();
      this.initUserParagraphs();
  }

  ngOnInit(): void {
    this.userState = this.userService.state.subscribe({
      next: val => this.userStateChanged(val),
      error: err => this.userServiceError(err)
    });
  }

  ngOnDestroy(): void {
    this.userState.unsubscribe();
  }
  
  private initGuestParagraphs(): void {
    this.guestParagraphs.push("Good day!");
    this.guestParagraphs.push("Please signup or login in order to operate Automated Stock Counselor");
  }
  
  private initUserParagraphs(): void {
    this.userParagraphs.push("Good day, <first-name> <last-name>!");
    this.userParagraphs.push("Automated Stock Counselor can assit you with a variety of tasks.");
    this.userParagraphs.push("For example, gathering financial data, calculating investment recommendation.");
    this.userParagraphs.push("You can also view the existing investment recommendations");
  }

  private updateFirstAndLastNamesInUserParagraphs(firstName: string, lastName: string): void {
    this.userParagraphs[0] = `Good day, ${firstName} ${lastName}`;
  }

  private userServiceError(err: Error): void {
    let errMsg = `userService has failed.\n${err}`;
    this.loggerService.error(GreetingComponent.name, "userServiceError", errMsg); 
  }
  
  private userStateChanged(val: ApplicativeUserState): void {
    if (val == ApplicativeUserState.LOGGED_IN) {
      let user = this.userService.user;
      this.updateFirstAndLastNamesInUserParagraphs(user.firstName, user.lastName);
      this.greetingForGuest.hide();
      this.greetingForUser.show();
    }
    else if (val == ApplicativeUserState.LOGGED_OUT) {
      this.greetingForUser.hide();
      this.greetingForGuest.show();
    }
    else {
      let errMsg = "userService has returned an unexpected ApplicativeUserState.";
      this.userServiceError(new Error(errMsg));
    }
  }
}
