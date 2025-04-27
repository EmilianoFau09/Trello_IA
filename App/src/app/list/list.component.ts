import {Component, EventEmitter, Input, Output, SimpleChanges} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {FormBuilder, FormGroup, ReactiveFormsModule} from "@angular/forms";
import {HttpService} from '../services/http.service';
import {HttpErrorResponse} from '@angular/common/http';
import {List} from '../models/list';

@Component({
  selector: 'app-list',
  standalone: true,
    imports: [
        NgForOf,
        NgIf,
        ReactiveFormsModule
    ],
  templateUrl: './list.component.html',
  styleUrl: './list.component.css'
})
export class ListComponent {
  @Input() list: List | undefined;
  @Output() closeModal: EventEmitter<void> = new EventEmitter<void>();
  @Output() refresh: EventEmitter<void> = new EventEmitter<void>();

  listForm: FormGroup;

  constructor(private httpService: HttpService, private fb: FormBuilder) {
    this.listForm = this.fb.group({
      title: [''],
      description: ['']
    });
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['list'] && this.list) {
      this.listForm.patchValue({
        title: this.list.title,
        description: this.list.description
      });
    }
  }

  onSubmit(): void {
    if (this.list && this.list.idList) {
      this.httpService.putList(
        this.list.idList,
        this.listForm.value.title,
        this.listForm.value.description,
      ).subscribe(
        (response: any): void => {
          this.close();
          this.refresh.emit();
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  close(): void {
    this.closeModal.emit();
  }

  iaDescription: string = "";

  summarizeContent(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.list) {
      this.httpService.summarizeContent(this.listForm.value.description).subscribe(
        (response: string): void => {
          this.iaDescription = response;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  expandContent(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.list) {
      this.httpService.expandContent(this.listForm.value.description).subscribe(
        (response: string): void => {
          this.iaDescription = response;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  rewriteAndCorrectContent(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.list) {
      this.httpService.rewriteAndCorrectContent(this.listForm.value.description).subscribe(
        (response: string): void => {
          this.iaDescription = response;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  generateVariations(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.list) {
      this.httpService.generateVariations(this.listForm.value.description).subscribe(
        (response: string[]): void => {
          let text: string = ""
          let n: number = 1;
          response.forEach((e: string): void => {
            text += "Alternativa " + n + ":\n" + e + "\n\n";
            n += 1;
          })
          this.iaDescription = text;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  correctContent(): void {
    this.iaDescription = "Espere a que se genere su respuesta."
    if (this.list) {
      this.httpService.correctContent(this.listForm.value.description).subscribe(
        (response: string): void => {
          this.iaDescription = response;
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }
}
