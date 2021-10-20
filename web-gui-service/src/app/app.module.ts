import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { HomepageComponent } from './homepage/homepage.component';
import { WebsiteMenuComponent } from './homepage/website-menu/website-menu.component';
import { DashboardComponent } from './homepage/dashboard/dashboard.component';
import { AcknowledgementsBoardComponent } from './homepage/acknowledgements-board/acknowledgements-board.component';
import { ActionAreaComponent } from './homepage/action-area/action-area.component';
import { CalculateInvestmentRecommendationComponent }
  from './homepage/action-area/calculate-investment-recommendation/calculate-investment-recommendation.component';
import { CollectStockDataComponent } from './homepage/action-area/collect-stock-data/collect-stock-data.component';
import { GreetingComponent } from './homepage/action-area/greeting/greeting.component';
import { LoginComponent } from './homepage/action-area/login/login.component';
import { SignupComponent } from './homepage/action-area/signup/signup.component';
import { GreetingForGuestDirective } from './homepage/action-area/greeting/greeting-for-guest.directive';
import { GreetingForUserDirective } from './homepage/action-area/greeting/greeting-for-user.directive';
import { SignupRequestContainerDirective } from './homepage/action-area/signup/signup-request-container.directive';
import { SignupRequestErrorContainerDirective } from './homepage/action-area/signup/signup-request-error-container.directive';
import { InvestmentFunctionalitiesMenuComponent } from './homepage/action-area/investment-functionalities-menu/investment-functionalities-menu.component';
import { CollectStockDataRequestContainerDirective } from './homepage/action-area/collect-stock-data/collect-stock-data-request-container.directive';
import { CollectStockDataRequestErrorContainerDirective } from './homepage/action-area/collect-stock-data/collect-stock-data-request-error-container.directive';
import { CollectStockDataResponseContainerDirective } from './homepage/action-area/collect-stock-data/collect-stock-data-response-container.directive';
import { CalculateInvestmentRecommendationRequestContainerDirective } from './homepage/action-area/calculate-investment-recommendation/calculate-investment-recommendation-request-container.directive';
import { CalculateInvestmentRecommendationRequestErrorContainerDirective } from './homepage/action-area/calculate-investment-recommendation/calculate-investment-recommendation-request-error-container.directive';
import { CalculateInvestmentRecommendationResponseContainerDirective } from './homepage/action-area/calculate-investment-recommendation/calculate-investment-recommendation-response-container.directive';

@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent,
    PageNotFoundComponent,
    HomepageComponent,
    WebsiteMenuComponent,
    DashboardComponent,
    AcknowledgementsBoardComponent,
    ActionAreaComponent,
    CalculateInvestmentRecommendationComponent,
    CollectStockDataComponent,
    GreetingComponent,
    LoginComponent,
    SignupComponent,
    GreetingForGuestDirective,
    GreetingForUserDirective,
    SignupRequestContainerDirective,
    SignupRequestErrorContainerDirective,
    InvestmentFunctionalitiesMenuComponent,
    CollectStockDataRequestContainerDirective,
    CollectStockDataRequestErrorContainerDirective,
    CollectStockDataResponseContainerDirective,
    CalculateInvestmentRecommendationRequestContainerDirective,
    CalculateInvestmentRecommendationRequestErrorContainerDirective,
    CalculateInvestmentRecommendationResponseContainerDirective
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  exports: [],
  providers: [
    GreetingForGuestDirective,
    GreetingForUserDirective,
    SignupRequestContainerDirective,
    SignupRequestErrorContainerDirective,
    CollectStockDataRequestContainerDirective,
    CollectStockDataRequestErrorContainerDirective,
    CollectStockDataResponseContainerDirective,
    CalculateInvestmentRecommendationRequestContainerDirective,
    CalculateInvestmentRecommendationRequestErrorContainerDirective,
    CalculateInvestmentRecommendationResponseContainerDirective
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
