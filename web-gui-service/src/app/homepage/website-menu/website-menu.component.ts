import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoggerService } from 'src/app/logger.service';
import { Logo } from 'src/app/logo';
import { LogoService } from 'src/app/logo.service';

import { ApplicativeUserState } from '../user-state';
import { UserService } from '../user.service';

import { WebsiteMenuStateService } from './state.service';

@Component({
  selector: 'app-homepage-website-menu',
  templateUrl: './website-menu.component.html',
  styleUrls: ['./website-menu.component.sass']
})
export class WebsiteMenuComponent implements OnDestroy, OnInit {

  public guestMode: boolean;
  public logo: Logo;

  private userState: Subscription;

  constructor(
    private loggerService: LoggerService,
    private logoService: LogoService,
    private userService: UserService,
    private websiteMenuStateService: WebsiteMenuStateService
    ) {
      this.logo = new Logo();
      this.guestMode = true;
      this.userState = new Subscription();
  }

  ngOnDestroy(): void {
    this.userState.unsubscribe();
  }

  ngOnInit(): void {
    this.logoService.getLogo().subscribe({
      next: val => this.nextLogo(val),
      error: err => this.logoServiceError(err)
    });
    this.userState = this.userService.state.subscribe({
      next: val => this.nextUserState(val),
      error: err => this.userServiceError(err)
    });
  }

  public login(): void {
    this.websiteMenuStateService.loginState();
  }

  public logout(): void {
    this.websiteMenuStateService.initialState();
    this.userService.logout();
  }

  public signup(): void {
    this.websiteMenuStateService.signupState();
  }

  private logoServiceError(err: Error): void {
    let errMsg = `logoService has failed.\n${err}`;
    this.loggerService.error(WebsiteMenuComponent.name, "logoServiceError", errMsg);
  }

  private nextLogo(val: Logo): void {
    this.logo = val;
  }

  private nextUserState(val: ApplicativeUserState): void {
    if (val == ApplicativeUserState.ANONYMOUS) {
      this.guestMode = true;
    }
    else if (val == ApplicativeUserState.LOGGED_IN) {
      console.log("Should change");
      this.guestMode = false;
    }
    else if (val == ApplicativeUserState.LOGGED_OUT) {
      this.guestMode = true;
    }
    else {
      let errMsg = `Unexpected ApplicativeUserState value.\nval:\t${val}`;
      this.userServiceError(new Error(errMsg));
    }
  }

  private userServiceError(err: Error): void {
    let errMsg = `userService has failed.\n${err}`;
    this.loggerService.error(WebsiteMenuComponent.name, "userServiceError", errMsg);
  }

}
