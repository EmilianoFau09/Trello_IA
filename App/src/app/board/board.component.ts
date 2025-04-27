import {Component} from '@angular/core';
import {HttpService} from '../services/http.service';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {List} from '../models/list';
import {Card} from '../models/card';
import {CreateCardFormComponent} from '../create-card-form/create-card-form.component';
import {NgForOf, NgIf} from '@angular/common';
import {CardComponent} from '../card/card.component';
import {CreateListFormComponent} from '../create-list-form/create-list-form.component';
import {ListComponent} from '../list/list.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';

@Component({
  selector: 'app-board',
  standalone: true,
  imports: [
    CreateCardFormComponent,
    NgIf,
    CardComponent,
    NgForOf,
    CreateListFormComponent,
    ListComponent,
    ReactiveFormsModule,
    FormsModule
  ],
  templateUrl: './board.component.html',
  styleUrl: './board.component.css'
})
export class BoardComponent {
  lists: List[] = [];
  boardTitle: string = "";
  boardTopic: string = ""
  topics: string[] = []

  isCreateCardFormOpen: boolean = false;
  selectedList: List | undefined;
  isCardOpen: boolean = false;
  selectedCard: Card | undefined;
  isCreateListFormOpen: boolean = false;
  isListOpen: boolean = false;

  constructor(private httpService: HttpService) {}

  ngOnInit(): void {
    this.getLists();
    this.getBoardTitle()
    this.getBoardTopic()
    this.getTopics()
  }

  openCreateCardForm(list: List): void {
    this.selectedList = list;
    this.isCreateCardFormOpen = true;
  }

  closeCreateCardForm(): void {
    this.selectedList = undefined;
    this.isCreateCardFormOpen = false;
  }

  openCard(card: Card): void {
    this.selectedCard = card;
    this.isCardOpen = true;
  }

  closeCard(): void {
    this.selectedCard = undefined;
    this.isCardOpen = false;
  }

  openCreateListForm(): void {
    this.isCreateListFormOpen = true;
  }

  closeCreateListForm(): void {
    this.isCreateListFormOpen = false;
  }

  openList(list: List): void {
    this.selectedList = list;
    this.isListOpen = true;
  }

  closeList(): void {
    this.selectedList = undefined;
    this.isListOpen = false;
  }

  getBoardTitle(): void {
    this.httpService.getBoardTitle().subscribe(
      (boardTitle: any): void => {
        this.boardTitle = boardTitle.boardTitle;
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    )
  }

  getBoardTopic(): void {
    this.httpService.getBoardTopic().subscribe(
      (boardTopic: any): void => {
        this.boardTopic = boardTopic.boardTopic;
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    )
  }

  getTopics(): void {
    this.httpService.getTopics().subscribe(
      (topics: any): void => {
        this.topics = topics.topics;
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    )
  }

  putBoardTitle(): void {
    this.httpService.putBoardTitle(this.boardTitle).subscribe(
      (response: any): void => {
        this.getBoardTitle();
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    )
  }

  putBoardTopic(): void {
    this.httpService.putBoardTopic(this.boardTopic).subscribe(
      (response: any): void => {
        this.getBoardTopic();
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    )
  }

  getLists(): void {
    this.httpService.getLists().subscribe(
      (lists: List[]): void => {
        this.lists = lists;
        this.getCards();
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    )
  }

  getCards(): void {
    this.httpService.getCards().subscribe(
      (cards: Card[]): void => {
        this.lists.forEach((list: List): void => {
          list.cards = cards.filter((card: Card): boolean => card.idList === list.idList);
        });
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    )
  }

  deleteList(idList: string | undefined): void {
    if (idList) {
      this.httpService.deleteList(idList).subscribe(
        (response: HttpResponse<BoardComponent[]>) => {
          this.getLists();
        }, (err: HttpErrorResponse) => {
          console.log(err);
        }
      )
    }
  }

  generateCardsForList(idList: string | undefined, listTitle: string, listDescription: string): void {
    if (idList) {
      const text: string = "Titulo de la lista: " + listTitle + " \nDescripcion de la lista: " + listDescription;
      this.httpService.generateCardsForList(text).subscribe(
        (response: any): void => {
          response.forEach((e: any): void => {
            this.postCard(idList, e.title, e.description);
          })
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  postCard(idList: string, title: string, description: string): void {
    this.httpService.postCard(
      description,
      idList,
      title
    ).subscribe(
      (response: any): void => {
        this.getLists();
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    );
  }

  generateListsForBoard(): void {
    this.httpService.generateListsForBoard().subscribe(
      (response: any): void => {
        response.forEach((e: any): void => {
          this.postList(e.title, e.description);
        })
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    );
  }

  postList(title: string, description: string): void {
    this.httpService.postList(
      title,
      description
    ).subscribe(
      (response: any): void => {
        this.getLists();
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    );
  }
}
