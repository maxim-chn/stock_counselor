import { Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

import { LoggerService } from 'src/app/logger.service';

import { UserService } from '../user.service';
import { ApplicativeUserState } from '../user-state';

import { WebsiteMenuState } from '../website-menu/state';
import { WebsiteMenuStateService } from '../website-menu/state.service';

import { InvestmentFunctionalitiesMenuState } from './investment-functionalities-menu/state';
import { InvestmentFunctionalitiesMenuStateService } from './investment-functionalities-menu/state.service';

@Component({
  selector: 'app-homepage-action-area',
  templateUrl: './action-area.component.html',
  styleUrls: ['./action-area.component.sass']
})
export class ActionAreaComponent implements OnDestroy, OnInit {

  public className: string;
  public showCalculateInvestmentRecommendation: boolean;
  public showCollectStockData: boolean;
  public showGreeting: boolean;
  public showLogin: boolean;
  public showSignup: boolean;

  private investmentFunctionalitiesMenuState: Subscription;
  private websiteMenuState: Subscription;
  private userState: Subscription;

  constructor(
    private loggerService: LoggerService,
    private investmentFunctionalitiesMenuStateService: InvestmentFunctionalitiesMenuStateService,
    private websiteMenuStateService: WebsiteMenuStateService,
    private userService: UserService
    ) {
      this.className = ActionAreaComponent.name;
      this.showCalculateInvestmentRecommendation = false;
      this.showCollectStockData = false;
      this.showGreeting = true;
      this.showLogin = false;
      this.showSignup = false;
      this.investmentFunctionalitiesMenuState = new Subscription();
      this.websiteMenuState = new Subscription();
      this.userState = new Subscription();
  }

  ngOnDestroy(): void {
    this.investmentFunctionalitiesMenuState.unsubscribe();
    this.websiteMenuState.unsubscribe();
    this.userState.unsubscribe();
  }

  ngOnInit(): void {
    this.investmentFunctionalitiesMenuState = this.investmentFunctionalitiesMenuStateService.state.subscribe({
      next: val => this.nextInvestmentFunctionalitiesMenuState(val),
      error: err => this.investmentFunctionalitiesMenuStateServiceError(err)
    });
    this.websiteMenuState = this.websiteMenuStateService.state.subscribe({
      next: val => this.nextWebsiteMenuState(val),
      error: err => this.websiteMenuStateServiceError(err)
    });
    this.userState = this.userService.state.subscribe({
      next: val => this.userStateChanged(val),
      error: err => this.userServiceError(err)
    });
  }

  private investmentFunctionalitiesMenuStateServiceError(err: Error): void {
    let errMsg = `InvestmentFunctionalitiesMenuStateService has failed.\n${err}`;
    this.loggerService.error(ActionAreaComponent.name, "investmentFunctionalitiesMenuStateServiceError", errMsg);
  }

  private nextInvestmentFunctionalitiesMenuState(val: InvestmentFunctionalitiesMenuState): void {
    if (val == InvestmentFunctionalitiesMenuState.COLLECT_STOCK_DATA) {
      this.showCollectStockDataComponent();
    }
    else if (val == InvestmentFunctionalitiesMenuState.CREATE_INVESTMENT_RECOMMENDATION) {
      this.showCalculateInvestmentRecommendationComponent();
    }
    else if (val == InvestmentFunctionalitiesMenuState.INITIAL) {
      if (!this.showGreeting) {
        this.showGreetingComponent();
      }
    }
    else {
      let errMsg = "An unexpected InvestmentFunctionalitiesMenuState has been returned.";
      this.investmentFunctionalitiesMenuStateServiceError(new Error(errMsg));
    }
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

  private showCalculateInvestmentRecommendationComponent(): void {
    this.showCalculateInvestmentRecommendation = true;
    this.showCollectStockData = false;
    this.showGreeting = false;
    this.showLogin = false;
    this.showSignup = false;
  }

  private showCollectStockDataComponent(): void {
    this.showCalculateInvestmentRecommendation = false;
    this.showCollectStockData = true;
    this.showGreeting = false;
    this.showLogin = false;
    this.showSignup = false;
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
    let errMsg = `WebsiteMenuStateService has failed.\n${err}`;
    this.loggerService.error(ActionAreaComponent.name, "websiteMenuStateServiceError", errMsg);
  }

  private userServiceError(err: Error): void {
    let errMsg = `${this.userService.className} has failed.\n${err}`;
    this.loggerService.error(this.className, "userServiceError", errMsg); 
  }
  
  private userStateChanged(val: ApplicativeUserState): void {
    if (val == ApplicativeUserState.LOGGED_IN) {
      this.showGreetingComponent();
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
