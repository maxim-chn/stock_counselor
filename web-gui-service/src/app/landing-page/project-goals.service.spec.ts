import { TestBed } from '@angular/core/testing';

import { ProjectGoalsService } from './project-goals.service';

describe('ProjectGoalsService', () => {
  let service: ProjectGoalsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ProjectGoalsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
