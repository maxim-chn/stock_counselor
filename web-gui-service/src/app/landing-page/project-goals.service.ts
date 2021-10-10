import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

import { ProjectGoal } from './project-goal';

@Injectable({
  providedIn: 'root'
})
export class ProjectGoalsService {
  
  private goals: Array<ProjectGoal>;

  constructor() {
    /**
     * @TODO replace logo image with proper base64 png encoding.
    */
    this.goals = [
      ProjectGoal.withAllAttributes(
        "Project Goal Icon",
        "data:image/png;base64,BROKEN_VALUE",
        "Reduce time invested into manual collection of financial data reports"
      ),
      ProjectGoal.withAllAttributes(
        "Project Goal Icon",
        "data:image/png;base64,BROKEN_VALUE",
        "Reduce time invested into manual inspection of financial data reports"
      ),
      ProjectGoal.withAllAttributes(
        "Project Goal Icon",
        "data:image/png;base64,BROKEN_VALUE",
        "Improve the investment strategy management"
      ),
      ProjectGoal.withAllAttributes(
        "Project Goal Icon",
        "data:image/png;base64,BROKEN_VALUE",
        "Monitor investment rules performance"
      )
    ]
  }

  public getGoals(): Observable<Array<ProjectGoal>> {
    return of(this.goals);
  }

}
