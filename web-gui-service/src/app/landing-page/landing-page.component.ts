import { Component, OnInit } from '@angular/core';

import { Copyright } from '../copyright';
import { LoggerService } from '../logger.service';
import { Logo } from '../logo';
import { LogoService } from '../logo.service';

import { Acknowledgement } from './acknowledgement';
import { AcknowledgementService } from './acknowledgement.service';
import { CopyrightService } from './copyright.service';
import { PrefaceParagraphsService } from './preface-paragraphs.service';
import { ProjectGoalsService } from './project-goals.service';
import { ProjectGoal } from './project-goal';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.sass']
})
export class LandingPageComponent implements OnInit {

  public acknowledgement: Acknowledgement;
  public copyrights: Array<Copyright>;
  public logo: Logo;
  public prefaceParagraphs: Array<string>;
  public projectGoals: Array<ProjectGoal>;
  public title: string;
  
  constructor(
    private acknowledgementService: AcknowledgementService,
    private copyrightsService: CopyrightService,
    private loggerService: LoggerService,
    private logoService: LogoService,
    private prefaceParagraphsService: PrefaceParagraphsService,
    private projectGoalsService: ProjectGoalsService
    ) {
      this.acknowledgement = new Acknowledgement();
      this.copyrights = [];
      this.logo = new Logo();
      this.prefaceParagraphs = [];
      this.projectGoals = [];
      this.title = "Stock Counselor Project"
  }

  ngOnInit(): void {
    this.acknowledgementService.getAcknowledgement().subscribe({
      next: val => this.nextAcknowledgement(val),
      error: err => this.acknowledgementServiceError(err)
    });
    this.copyrightsService.getCopyrights().subscribe({
      next: collection => collection.forEach(val => this.nextCopyright(val)),
      error: err => this.copyrightsServiceError(err)
    });
    this.logoService.getLogo().subscribe({
      next: val => this.nextLogo(val),
      error: err => this.logoServiceError(err)
    });
    this.prefaceParagraphsService.getParagraphs().subscribe({
      next: collection => collection.forEach(val => this.nextPrefaceParagraph(val)),
      error: err => this.prefaceParagraphsServiceError(err)
    });
    this.projectGoalsService.getGoals().subscribe({
      next: collection => collection.forEach(val => this.nextProjectGoal(val)),
      error: err => this.projectGoalsServiceError(err)
    });
  }

  private acknowledgementServiceError(err: Error): void {
    let errMsg = `Failed.\n${err}`;
    this.loggerService.error(LandingPageComponent.name, "acknowledgementServiceError", errMsg);
  }

  private copyrightsServiceError(err: Error): void {
    let errMsg = `Failed.\n${err}`;
    this.loggerService.error(LandingPageComponent.name, "copyrightsService", errMsg);
  }
  
  private logoServiceError(err: Error): void {
    let errMsg = `Failed.\n${err}`;
    this.loggerService.error(LandingPageComponent.name, "logoServiceError", errMsg);
  }

  private nextAcknowledgement(val: Acknowledgement): void {
    this.acknowledgement = val;
  }

  private nextCopyright(val: Copyright): void {
    this.copyrights.push(val);
  }

  private nextLogo(val: Logo): void {
    this.logo = val;
  }

  private nextPrefaceParagraph(val: string): void {
    this.prefaceParagraphs.push(val);
  }

  private nextProjectGoal(val: ProjectGoal): void {
    this.projectGoals.push(val);
  }

  private prefaceParagraphsServiceError(err: Error) {
    let errMsg = `Failed.\n${err}`;
    this.loggerService.error(LandingPageComponent.name, "prefaceParagraphsServiceError", errMsg);
  }

  private projectGoalsServiceError(err: Error) {
    let errMsg = `Failed.\n${err}`;
    this.loggerService.error(LandingPageComponent.name, "projectGoalsServiceError", errMsg);
  }

}
