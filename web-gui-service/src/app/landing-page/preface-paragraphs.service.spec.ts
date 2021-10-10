import { TestBed } from '@angular/core/testing';

import { PrefaceParagraphsService } from './preface-paragraphs.service';

describe('PrefaceParagraphsService', () => {
  let service: PrefaceParagraphsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PrefaceParagraphsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
