from pdiplom.issuer_diplom import broadcast_tx


def recall_diplom(uid):
    err = broadcast_tx(uid, 'deleted')
    return err