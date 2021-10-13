import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoggerService } from 'src/app/logger.service';
import { WebsiteMenuState } from '../website-menu/state';
import { WebsiteMenuStateService } from '../website-menu/state.service';

@Component({
  selector: 'app-homepage-action-area',
  templateUrl: './action-area.component.html',
  styleUrls: ['./action-area.component.sass']
})
export class ActionAreaComponent implements OnDestroy, OnInit {

  public showCalculateInvestmentRecommendation: boolean;
  public showCollectStockData: boolean;
  public showGreeting: boolean;
  public showLogin: boolean;
  public showSignup: boolean;

  private websiteMenuState: Subscription;

  constructor(
    private loggerService: LoggerService,
    private websiteMenuStateService: WebsiteMenuStateService
    ) {
      this.showCalculateInvestmentRecommendation = false;
      this.showCollectStockData = false;
      this.showGreeting = true;
      this.showLogin = false;
      this.showSignup = false;
      this.websiteMenuState = new Subscription();
  }

  ngOnDestroy(): void {
    this.websiteMenuState.unsubscribe();
  }

  ngOnInit(): void {
    this.websiteMenuState = this.websiteMenuStateService.state.subscribe({
      next: val => this.nextWebsiteMenuState(val),
      error: err => this.websiteMenuStateServiceError(err)
    });
  }

  private nextWebsiteMenuState(val: WebsiteMenuState): void {
    if (val == WebsiteMenuState.INITIAL) {
      this.showGreetingComponent();
    }
    else if (val == WebsiteMenuState.LOGIN) {
      this.showLoginComponent();
    }
    else if (val == WebsiteMenuState.SIGNUP) {
      this.showSignupComponent();
    }
    else {
      let errMsg = "An unexpected WebsiteMenuState was returned.";
      this.websiteMenuStateServiceError(new Error(errMsg));
    }
  }

  private showGreetingComponent(): void {
    this.showCalculateInvestmentRecommendation = false;
    this.showCollectStockData = false;
    this.showGreeting = true;
    this.showLogin = false;
    this.showSignup = false;
  }

  private showLoginComponent(): void {
    this.showCalculateInvestmentRecommendation = false;
    this.showCollectStockData = false;
    this.showGreeting = false;
    this.showLogin = true;
    this.showSignup = false;
  }

  private showSignupComponent(): void {
    this.showCalculateInvestmentRecommendation = false;
    this.showCollectStockData = false;
    this.showGreeting = false;
    this.showLogin = false;
    this.showSignup = true;
  }

  private websiteMenuStateServiceError(err: Error): void {
    let errMsg = `websiteMenuStateService has failed.\n${err}`;
    this.loggerService.error(ActionAreaComponent.name, "websiteMenuStateServiceError", errMsg);
  }

}
