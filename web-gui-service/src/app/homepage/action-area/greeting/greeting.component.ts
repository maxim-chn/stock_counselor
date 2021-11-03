import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoggerService } from 'src/app/logger.service';

import { UserService } from '../../user.service';
import { ApplicativeUserState } from '../../user-state';

import {
  hideParagraphsForGuestContainer,
  initialClassesForParagraphsForGuestContainer,
  showParagraphsForGuestContainer,
  WithParagraphsForGuestContainer
} from './with-paragraphs-for-guest-container';

import {
  hideParagraphsForUserContainer,
  initialClassesForParagraphsForUserContainer,
  showParagraphsForUserContainer,
  WithParagraphsForUserContainer
} from './with-paragraphs-for-user-container';

@Component({
  selector: 'action-area-greeting',
  templateUrl: './greeting.component.html',
  styleUrls: ['./greeting.component.sass']
})
export class GreetingComponent implements
  OnInit, 
  OnDestroy,
  WithParagraphsForGuestContainer,
  WithParagraphsForUserContainer
{

  public animationTimeout: number;
  public className: string;
  public guestParagraphs: Array<string>;
  @Input() paragraphsForGuestContainerClasses: Array<string>;
  @Input() paragraphsForUserContainerClasses: Array<string>;
  public userParagraphs: Array<string>;
  
  private userState: Subscription;

  constructor(private loggerService: LoggerService, private userService: UserService) {
    this.animationTimeout = 100;
    this.className = GreetingComponent.name;
    this.guestParagraphs = [];
    this.userParagraphs = [];
    this.userState = new Subscription();
    this.initGuestParagraphs();
    this.initUserParagraphs();
    this.paragraphsForGuestContainerClasses = initialClassesForParagraphsForGuestContainer();
    this.paragraphsForUserContainerClasses = initialClassesForParagraphsForUserContainer();
  }

  ngOnInit(): void {
    hideParagraphsForUserContainer(this);
    showParagraphsForGuestContainer(this);
    this.userState = this.userService.state.subscribe({
      next: val => this.userStateChanged(val),
      error: err => this.userServiceError(err)
    });
  }

  ngOnDestroy(): void {
    hideParagraphsForUserContainer(this);
    hideParagraphsForGuestContainer(this);
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
    let errMsg = `${this.userService.className} has failed.\n${err}`;
    this.loggerService.error(this.className, "userServiceError", errMsg); 
  }
  
  private userStateChanged(val: ApplicativeUserState): void {
    if (val == ApplicativeUserState.LOGGED_IN) {
      let user = this.userService.user;
      this.updateFirstAndLastNamesInUserParagraphs(user.firstName, user.lastName);
      hideParagraphsForGuestContainer(this);
      showParagraphsForUserContainer(this);
    }
    else if (val == ApplicativeUserState.LOGGED_OUT) {
      hideParagraphsForUserContainer(this);
      showParagraphsForGuestContainer(this);
    }
    else if (val == ApplicativeUserState.ANONYMOUS) {
      // Do nothing
    }
    else {
      let errMsg = `Unexpected ApplicativeUserState has been returned.\nVal:\t${val}`;
      this.userServiceError(new Error(errMsg));
    }
  }
}
