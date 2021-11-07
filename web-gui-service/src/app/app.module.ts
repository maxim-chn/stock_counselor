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
import { InvestmentFunctionalitiesMenuComponent }
  from './homepage/action-area/investment-functionalities-menu/investment-functionalities-menu.component';

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
    InvestmentFunctionalitiesMenuComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule
  ],
  exports: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
