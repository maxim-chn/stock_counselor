import { Component, OnInit } from '@angular/core';

import { LoggerService } from 'src/app/logger.service';
import { isStockAcronymLegal } from 'src/app/validations';

import { BackendApiService } from '../backend-api.service';

import { CollectStockDataRequestContainerDirective } from './collect-stock-data-request-container.directive';
import { CollectStockDataRequestErrorContainerDirective } from './collect-stock-data-request-error-container.directive';
import { CollectStockDataResponseContainerDirective } from './collect-stock-data-response-container.directive';

@Component({
  selector: 'action-area-collect-stock-data',
  templateUrl: './collect-stock-data.component.html',
  styleUrls: ['./collect-stock-data.component.sass']
})
export class CollectStockDataComponent implements OnInit {

  public className: string;
  public errorMessage: string;
  public responseMessage: string;
  public stockAcronym: string;

  constructor(
    private backendApiService: BackendApiService,
    private loggerService: LoggerService,
    private requestContainerDirective: CollectStockDataRequestContainerDirective,
    private requestErrorContainerDirective: CollectStockDataRequestErrorContainerDirective,
    private responseContainerDirective: CollectStockDataResponseContainerDirective
  ) {
    this.className = CollectStockDataComponent.name;
    this.errorMessage = "No error";
    this.responseMessage = "No response";
    this.stockAcronym = "No value";
    this.displayRequestContainer();
  }

  ngOnInit(): void {
  }

  public dismissErrorMessage(): void {
    this.displayRequestContainer();
  }

  public dismissResponseMessage(): void {
    this.displayRequestContainer();
  }

  public submit(): void {
    if (isStockAcronymLegal(this.stockAcronym)) {
      this.backendApiService.collectStockData(this.stockAcronym).subscribe({
        next: val => this.nextBackendResponse(val),
        error: err => this.backendApiServiceError(err)
      });
    }
    else {
      let errMsg = "You have used a wrong stock acronym format.\nThe right format, for example, is msft or MSFT.";
      this.displayRequestErrorContainer(errMsg);
    }
  }

  public stockAcronymUpdated(event: Event): void {
    this.stockAcronym = (<HTMLInputElement>event.target).value;
  }

  private backendApiServiceError(err: Error): void {
    let errMsg = `${this.backendApiService.className} has failed.\n${err}`;
    this.loggerService.error(this.className, "backendApiServiceError", errMsg);
    this.displayRequestErrorContainer(errMsg);
  }

  private displayRequestContainer(): void {
    this.errorMessage = "No error";
    this.responseMessage = "No response";
    this.requestContainerDirective.show();
    this.requestErrorContainerDirective.hide();
    this.responseContainerDirective.hide();
  }

  private displayRequestErrorContainer(errorMessage: string): void {
    this.errorMessage = errorMessage;
    this.responseMessage = "No response";
    this.requestContainerDirective.hide();
    this.requestErrorContainerDirective.show();
    this.responseContainerDirective.hide();
  }

  private displayResponseContainer(responseMessage: string): void {
    this.errorMessage = "No error";
    this.responseMessage = responseMessage;
    this.requestContainerDirective.hide();
    this.requestErrorContainerDirective.hide();
    this.responseContainerDirective.show();
  }

  private nextBackendResponse(val: string): void {
    this.displayResponseContainer(val);
  }

}
