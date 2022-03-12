import flair


NERtagger = flair.models.SequenceTagger.load('flair/ner-english-ontonotes-large')


def generate_entities(sentence):

    entities = [ span.to_dict() for span in sentence.get_spans() ]
    for entity in entities:
        entity['labels'] = entity['labels'][0].to_dict()

    return entities


def perform_ner(emails):

    emails['sentences'] = emails['cleaned_body'].apply(flair.data.Sentence)

    NERtagger.predict(emails['sentences'].to_list())

    emails['entities']  = emails['sentences'].apply(generate_entities)


    return emails
