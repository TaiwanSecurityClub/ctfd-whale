from flask import Blueprint

from CTFd.models import (
    db,
    Flags,
)
from CTFd.plugins.dynamic_challenges import DynamicValueChallenge
from CTFd.utils import user as current_user
from .models import WhaleContainer, DynamicDockerChallenge
from .utils.control import ControlUtil


class DynamicValueDockerChallenge(DynamicValueChallenge):
    id = "dynamic_docker"  # Unique identifier used to register challenges
    name = "dynamic_docker"  # Name of a challenge type
    # Blueprint used to access the static_folder directory.
    blueprint = Blueprint(
        "ctfd-whale-challenge",
        __name__,
        template_folder="templates",
        static_folder="assets",
    )
    challenge_model = DynamicDockerChallenge

    @classmethod
    def read(cls, challenge):
        challenge = DynamicDockerChallenge.query.filter_by(id=challenge.id).first()
        data = super().read(challenge)
        data.update({
            "memory_limit": challenge.memory_limit,
            "cpu_limit": challenge.cpu_limit,
            "dynamic_score": challenge.dynamic_score,
            "docker_image": challenge.docker_image,
            "redirect_type": challenge.redirect_type,
            "redirect_port": challenge.redirect_port,
        })
        return data

    @classmethod
    def update(cls, challenge, request):
        challenge = super().update(challenge, request)

        if challenge.dynamic_score != 1:
            challenge.value = challenge.initial

        db.session.commit()
        return challenge

    @classmethod
    def attempt(cls, challenge, request):
        data = request.form or request.get_json()
        submission = data["submission"].strip()

        flags = Flags.query.filter_by(challenge_id=challenge.id).all()

        if len(flags) > 0:
            return super().attempt(challenge, request)
        else:
            user_id = current_user.get_current_user().id
            container = WhaleContainer.query.filter_by(user_id=user_id, challenge_id=challenge.id).first()
            if container == None:
                return False, "Please solve it during the container is running"

            if container.flag == submission:
                return True, "Correct"
            return False, "Incorrect"

    @classmethod
    def solve(cls, user, team, challenge, request):
        super().solve(user, team, challenge, request)
        
        if challenge.dynamic_score != 1:
            challenge.value = challenge.initial

        db.session.commit()

    @classmethod
    def delete(cls, challenge):
        for container in WhaleContainer.query.filter_by(
            challenge_id=challenge.id
        ).all():
            ControlUtil.try_remove_container(container.user_id)
        super().delete(challenge)
