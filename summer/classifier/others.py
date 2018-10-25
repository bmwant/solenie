from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB




def main():
    from summer.classifier.naive_bayes import get_labeled_review_data
    from summer.partitioner import DistributionPartitioner
    from froppyland.enums import SentimentEnum

    def pred(review):
        return review['sentiment'] == SentimentEnum.GOOD

    partitioner = DistributionPartitioner(reviews, pred=pred, ratio=0.85)
    partitioner.partition()


    MNB_classifier = SklearnClassifier(MultinomialNB())
    train_data = get_labeled_review_data(
        partitioner.training_data,
        feature_finder.find_features,
    )
    test_data = get_labeled_review_data(
        partitioner.test_data,
        feature_finder.find_features,
    )
    classifier.train(train_data)
    accuracy = classifier.accuracy(test_data)
    print('Accuracy: {:.2f}'.format(accuracy*100))
    classifier.show_top_features()
    classifier.save()




if __name__ == '__main__':
    main()
