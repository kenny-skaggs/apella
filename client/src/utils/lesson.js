import * as d3 from "d3";

const classSize = 10;

function buildResponseMap(responseList) {
    const responseMap = {};
    responseList.forEach((response) => {
        responseMap[response.user_id] = response
    });
    return responseMap
}

class IdCounts {
    constructor() {
        this.counts = {}
    }
    increment(id) {
        if (this.counts[id] === undefined) {
            this.counts[id] = 1;
        } else {
            this.counts[id] += 1;
        }
    }
    decrement(id) {
        if (this.counts[id] !== undefined) {
            this.counts[id] -= 1;
        }
    }
}

class ResponseDataView {
    constructor(responseList, questionId) {
        this.responseMap = buildResponseMap(responseList)
        this.questionId = questionId;
    }
}

class ParagraphResponseDataView extends ResponseDataView{
    updateResponse(response) {
        this.responseMap[response.user_id] = response;
        this.renderDetailedDisplay();
    }

    renderDetailedDisplay() {
        const thisTracker = this;

        d3.selectAll(`.apella-responses[questionId="${this.questionId}"]`)
            .selectAll('div.student-response')
            .data(Object.values(studentMap))
            .join('div')
            .attr('class', 'student-response paragraph')
            .html(function(student) {
                const response = thisTracker.responseMap[student.id];
                if (response === undefined) {
                    return `<div class="name">${student.username}</div>`;
                } else {
                    return `<div class="name">${student.username}</div>
                            <div class="answer"><span>${response.text}</span></div>`;
                }
            });
    }
}

class InlineTextResponseDataView extends ResponseDataView {
    updateResponse(response) {
        this.responseMap[response.user_id] = response;
        this.renderDetailedDisplay();
    }

    renderDetailedDisplay() {
        const thisTracker = this;

        d3.selectAll(`.apella-responses[questionId="${this.questionId}"]`)
            .selectAll('div.student-response')
            .data(Object.values(studentMap))
            .join('div')
            .attr('class', 'student-response inline-text')
            .html(function(student) {
                const response = thisTracker.responseMap[student.id];
                if (response === undefined) {
                    return `<div class="name">${student.username}</div>`;
                } else {
                    return `<div class="name">${student.username}</div>
                            <div class="answer"><span>${response.text}</span></div>`;
                }
            });
    }
}

class ChoiceResponseDataView extends ResponseDataView {
    constructor(responseList, questionId, $questionElement) {
        super(responseList, questionId)

        this.optionIndicatorMap = {};
        $questionElement.find('.question-choice').each((i, node) => {
            this.optionIndicatorMap[$(node).attr('option-id')] = String.fromCharCode(i + 65);
        });

        this.#buildSummary();
    }

    #buildSummary() {
        this.selectedOptionCounts = new IdCounts();
        Object.values(this.responseMap).forEach((response) => {
            this.#addResponseToSummary(response);
        });
    }

    #addResponseToSummary(response) {
        response.selected_option_ids.forEach((selectedId) => this.selectedOptionCounts.increment(selectedId));
    }

    #removeUserResponseFromSummary(userId) {
        const response = this.responseMap[userId];
        response.selected_option_ids.forEach((selectedId) => this.selectedOptionCounts.decrement(selectedId));
    }

    renderSummary() {
        for (const [optionId, answeredCount] of Object.entries(this.selectedOptionCounts.counts)) {
            this.#renderChoiceOptionSummary(optionId, answeredCount);
        }
    }

    renderDetailedDisplay() {
        const thisTracker = this;

        d3.selectAll(`.apella-responses[questionId="${this.questionId}"]`)
            .selectAll('div.student-response')
            .data(Object.values(studentMap))
            .join('div')
            .attr('class', 'student-response choice')
            .html(function(student) {
                const response = thisTracker.responseMap[student.id];
                if (response === undefined || response.selected_option_ids.length === 0) {
                    return `<div class="name">${student.username}</div>`;
                } else {
                    let response_selections = ''
                    for (const optionId of response.selected_option_ids) {
                        response_selections += thisTracker.optionIndicatorMap[optionId];
                    }
                    return `<div class="name">${student.username}</div>
                            <div class="selection"><span>${response_selections}</span></div>`;
                }
            })
    }

    updateResponse(response) {
        if (this.responseMap[response.user_id] !== undefined) {
            this.#removeUserResponseFromSummary(response.user_id);
        }
        this.responseMap[response.user_id] = response;
        this.#addResponseToSummary(response);
        this.renderSummary();
        this.renderDetailedDisplay();
    }

    #renderChoiceOptionSummary(optionId, answered_count) {
        var myScale = d3.scaleLinear()
            .domain([0, classSize])
            .range([0, 100]);
        d3.selectAll(`.question-choice[option-id="${optionId}"] .response-chart`)
          .selectAll('rect')
          .data([answered_count])
          .join('rect')
            .transition()
          .attr('width', function(d) {
            return `${myScale(d)}%`;
          });
    }
}

const questionResponseTrackers = {};
const studentMap = {};

function toggleDetailedResponseDisplay(event) {
    const $targetElement = $(event.currentTarget);
    const questionId = $targetElement.attr('questionId');
    const questionType = $targetElement.attr('type')
    const responseTracker = questionResponseTrackers[questionId];
    let $expandedDisplay = $(`.apella-responses[questionId="${questionId}"]`)

    if ($expandedDisplay.length === 0) {
        $targetElement.after(
            `<div class="apella-responses ${questionType}" questionId="${questionId}"></div>`
        )
        if (responseTracker !== undefined) {
            responseTracker.renderDetailedDisplay();
        }
    } else {
        $expandedDisplay.toggle();
    }
}

export default {
    initialize(studentList) {
        $('body').on('click', '.apella-question', toggleDetailedResponseDisplay);
        for (const student of studentList) {
            studentMap[student.id] = student;
        }
    },
    initializeDisplays(response_map) {
        for (const [questionId, responseList] of Object.entries(response_map)) {
            const $questionElement = $(`.apella-question[questionId="${questionId}"]`);
            const questionType = $questionElement.attr('type');
            let tracker;
            if (questionType === 'choice') {
                tracker = new ChoiceResponseDataView(responseList, questionId, $questionElement);
                tracker.renderSummary();
            } else if (questionType === 'paragraph') {
                tracker = new ParagraphResponseDataView(responseList, questionId);
            } else if (questionType === 'inline-text') {
                tracker = new InlineTextResponseDataView(responseList, questionId);
            }
            if (tracker !== undefined) {
                questionResponseTrackers[questionId] = tracker;
            }
        }
    },
    updateResponse(questionId, response) {
        questionResponseTrackers[questionId].updateResponse(response);
    }
}
