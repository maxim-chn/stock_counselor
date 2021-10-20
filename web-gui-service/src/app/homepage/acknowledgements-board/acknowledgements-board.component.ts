import { Component, OnInit } from '@angular/core';

import { CopyrightService } from './copyright.service';

import { Copyright } from 'src/app/copyright';
import { LoggerService } from 'src/app/logger.service';

@Component({
  selector: 'app-homepage-acknowledgements-board',
  templateUrl: './acknowledgements-board.component.html',
  styleUrls: ['./acknowledgements-board.component.sass']
})
export class AcknowledgementsBoardComponent implements OnInit {

  public className: string;
  public copyrights: Array<Copyright>;

  constructor(
    private copyrightService: CopyrightService,
    private loggerService: LoggerService
    ) {
      this.className = AcknowledgementsBoardComponent.name;
      this.copyrights = [];
  }

  ngOnInit(): void {
    this.copyrightService.getCopyrights().subscribe({
      next: collection => collection.forEach(val => this.nextCopyright(val)),
      error: err => this.copyrightServiceError(err)
    });
  }

  private copyrightServiceError(err: Error): void {
    let errMsg = `${this.copyrightService.className} has failed.\n${err}`;
    this.loggerService.error(this.className, "copyrightServiceError", errMsg);
  }

  private nextCopyright(val: Copyright): void {
    this.copyrights.push(val);
  }

}
